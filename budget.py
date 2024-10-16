from core import Core


class Budget( self ):
    def set_budget( self, schedule, scenario_idx ):
        search_msg = '이 시스템은 유능한 콘텐츠 예산 분석가입니다.'
        search_msg += '다음 스케줄을 보고 예산을 디테일하게 짜주세요.'
        search_msg += '예산 결과는 표로 보여주세요.'
        search_msg += '표의 헤더는 "항목, 기간, 세부항목, 예산"으로만 설정해주세요.'
        search_msg += '표의 맨 마지막에는 총 예산을 넣어주세요.'
        search_msg += '예산은 넷플릭스 상업영화를 기준으로 한화로 책정해주세요.'
        search_msg += '다른 어떠한 추가 문장이나 설명도 출력하지 말고, 반드시 표 형식으로만 답변하세요.'
        search_msg += '스케줄 : {schedule}'

        chain = self.chain(search_msg)
        response = chain.invoke( {'schedule':schedule} )
        
        load_budget = self.db.load_budget( scenario_idx )

        if not load_budget:
            self.db.insert_budget( response, scenario_idx )
        else:
            self.db.update_budget( response, scenario_idx )

        return response
    


