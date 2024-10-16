from core import Core

class Concept( Core ):
    def drawing_concept( self , synop):
        content = '이 시스템은  한국 영화의 컨셉 아티스트 입니다.'
        content += '이 시스템은 콘텐츠 정책을 준수 합니다.'
        content += '아래의 시놉시스에서 대표적인 장면 하나를 선택해서 이미지를 그려주세요.'
        content += '인물이 등장할경우 얼굴이 일그러지지 않게 그려주세요.'
        content += '등장인물의 얼굴은 모두 한국인 입니다.'
        content += '이미지에는 영어, 한글등 어떤 글자가 들어 가지 않게 그려주세요.'
        content += '{}\n'.format( synop )
        response = self.oai_client.images.generate(
            model = 'dall-e-3',
            prompt = content,
            n = 1,
            size = '1024x1024',
            quality = 'standard',
            style = 'natural'
        )
        image_url = response.data[0].url
        image_url_get = requests.get(image_url)

        img_uid = str(shortuuid.uuid())
        img_path = f'./tmp/concept/{img_uid}.png'
        with open(img_path, 'wb') as f:
            f.write( image_url_get.content )
        return img_path





