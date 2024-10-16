from core import Core

class Character( Core ):    
    def dev_character( self, scenario, scenario_idx ):
        search_msg = '이 시스템은 유능한 캐릭터 분석가 입니다.'
        search_msg += '다음 시나리오를 모두 읽고 주요 캐릭터들의 나이, 직업, 외형, 성격을 자세하게 분석해주세요.'
        search_msg += '제목, 장면 번호 등 다른 건 작성하지 말고 오로지 캐릭터 분석 내용만 보여주세요.'
        search_msg += '작성예시를 반드시 지켜서 작성해주세요.'
        search_msg += '내용 : {scenario}'
        search_msg += '작성예시)'
        search_msg += '### 0. 캐릭터 이름'
        search_msg += '- 나이: 언급된 나이 혹은 성격과 행동을 통해 유추한 나이만 작성'
        search_msg += '- 직업: 언급된 직업명 혹은 성격과 행동을 통해 유추한 직업명만 작성'
        search_msg += '- 외형: 성격과 행동을 통해 외형을 유추하고 이미지를 그릴 수 있을 정도로 구체적으로 묘사. 주어 없이 작성'
        search_msg += '- 성격: 구체적인 캐릭터 성격 설명. 주어 없이 작성'

        chain = self.chain(search_msg)
        response = chain.invoke( {'scenario':scenario} )
        
        load_character = self.db.load_character( scenario_idx )

        if not load_character:
            self.db.insert_character( response, scenario_idx )
        else:
            self.db.update_character( response, scenario_idx )

        return response
