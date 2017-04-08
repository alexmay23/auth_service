import os
import uuid
from binascii import hexlify
from asynclib.database.mongo import MongoDBManager, auto_reconnect
from asynclib.utils.functions import filter_only_keys

from service.instances import service
from service.lib import password_hash, date_or_now


class UserDBManager(MongoDBManager):
    def __init__(self):
        super(UserDBManager, self).__init__(collection_name='user', mongo_retriever=service)

    def generate_secret(self):
        return hexlify(os.urandom(12)).decode()

    async def create(self, identity, identity_type, password, timestamp=None):
        result = await self._create({
            'secret': self.generate_secret(),
            'password': password_hash(password),
            'identities': [{
                'type': identity_type,
                'value': identity,
                'verified': False,
                'uid': str(uuid.uuid4())
            }],
            'uid': await self.generate_id(),
            'timestamp': date_or_now(timestamp),
        })
        return result

    async def update(self, _id, **kwargs):
        return await self.update_one_denormalized({'_id': _id}, {'$set': filter_only_keys(kwargs,
                                                                                          ['timezone', 'locale'])})

    @auto_reconnect
    async def generate_id(self):
        cursor = self.db.find({}).skip(0).limit(1).sort([('uid', - 1)])
        if await cursor.count() == 0:
            return 1
        result = await cursor.to_list(1)
        return result[0].get('uid') + 1

    @auto_reconnect
    async def append_identity(self, user_id, identity_type, value):
        result = await self.db.update_one({'_id': user_id}, {
            'type': identity_type,
            'uid': str(uuid.uuid4()),
            'value': value,
            'verified': False
        })
        return result

    @auto_reconnect
    async def set_password(self, _id, password):
        await self.db.update_one({'_id': _id}, {'$set': {'password': password_hash(password)}})

    @auto_reconnect
    async def create_verification_context(self, uid, verification_context):
        await self.db.update_one({'identities.uid': uid}, {'$set':
                                                               {
                                                                   'identities.$.verification_context': verification_context}})

    @auto_reconnect
    async def verify(self, uid):
        await self.db.update_one({'identities.uid': uid}, {'$set': {'identities.$.verified': True},
                                                           '$unset': {'identities.$.verification_context': 1}})

    @auto_reconnect
    async def get_by_identity(self, identity):
        result = await self.db.find_one({'identities.value': identity})
        return result
