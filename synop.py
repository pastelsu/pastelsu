# :coding: utf-8

from core import Core


class Synop( Core ):
    def write(self, *key):
        key_list = key
        key_join = ','.join( key_list  )
        search_msg = '{key_join} 이런 내용의 시놉시스를 작성해줘.'
        search_msg += '제목같은 다른 내용은 출력하지 말고 시놉시스의 내용만 출력'
        chain = self.chain( search_msg )
        response = chain.invoke({'key_join':key_join}  )
        self.synop = response
        self.db.insert_synop( response, key_join )
        return response
        
