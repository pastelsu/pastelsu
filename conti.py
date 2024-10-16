from core import Core

import re
import requests
import shortuuid
import json
import urllib
import base64

from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment

from io import BytesIO

class Conti( Core ):
    def draw_conti( self, scenario, scenario_idx ):
        scene_pattern = re.compile(r'\#\#\# 장면 \d+:')

        scenes = scene_pattern.split(scenario)
        scene_titles = scene_pattern.findall(scenario)

        scene_list = [f"{title.strip()} {scene.strip()}" for title, scene in zip(scene_titles, scenes[1:])]

        load_conti = self.db.load_conti( scenario_idx )

        sd_server_url = 'http://10.0.80.94:7861'

        prompt = "이 시스템은 유능한 시나리오 축약 전문가입니다."
        prompt += "다음에 오는 내용을 영어로 한 문장으로 압축해서 stable diffusion 프롬프트를 작성해주세요."
        prompt += "다른 건 아무것도 출력하지 말고 오직 영어 프롬프트만 출력해주세요."
        prompt += "내용 : {scene}"

        for num, scene in enumerate(scene_list):
            chain = self.chain(prompt)
            response = chain.invoke( {'scene':scene} )

            if num == 0:
                seed = -1
            
            payload = {
                "prompt": f"cconti, sketch of {response} <lora:cconti:1>",
                "negative_prompt": "",
                "seed": seed,
                "steps": 20,
                "width": 1024,
                "height": 512,
                "cfg_scale": 7,
                "sampler_name": "Euler a",
                "n_iter": 1,
                "batch_size": 1,
            }

            data = json.dumps(payload).encode('utf-8')
            request = urllib.request.Request(
                f'{sd_server_url}/sdapi/v1/txt2img',
                headers={'Content-Type': 'application/json'},
                data=data,
            )
            image_url = urllib.request.urlopen(request)
            image = json.loads(image_url.read().decode('utf-8'))

            img_uid = str(shortuuid.uuid())
            img_path = f'./tmp/conti/scene{num+1}_{ img_uid }.png'
            with open(img_path, "wb") as file:
                file.write(base64.b64decode(image.get('images')[0]))
            
            seed_info = json.loads(image.get('info'))
            seed = seed_info['seed'] 

            if not load_conti:
                self.db.insert_conti( scene, img_path, scenario_idx )
            else:
                self.db.update_conti( scene, img_path, scenario_idx )

    def draw_conti_dall_e( self, scenario, scenario_idx ):
        scene_pattern = re.compile(r'\#\#\# 장면 \d+:')

        scenes = scene_pattern.split(scenario)
        scene_titles = scene_pattern.findall(scenario)

        scene_list = [f"{title.strip()} {scene.strip()}" for title, scene in zip(scene_titles, scenes[1:])]

        prompt_ori = '이 시스템은 영화 콘티작가 입니다.다음 시나리오 일부를 실사 이미지화 해주세요.'
        prompt_ori += "다음에 오는 내용에서 중요 장면 1개를 선정한 후 반드시 아래의 스타일에 맞춰 그려주세요"
        prompt_ori += "만약 컨텐츠 정책이 위반되었다면 반드시 정책을 준수해서 다시 장면 선정을 한 후 이미지를 재생성해주세요."
        prompt_ori += "스타일 : 흑색의 크로키 스타일 스케치, 본질과 감정을 담아낸 부드럽고 표현적인 선, 간결한 배경, 자연스러운 느낌"

        load_conti = self.db.load_conti( scenario_idx )

        for data in scene_list:
            prompt = prompt_ori

            prompt += f"내용 : {data}"
            prompt += "만약 컨텐츠 정책이 위반되었다면 반드시 정책을 준수할 때까지 다시 장면을 선정해서 이미지를 재생성해주세요."

            response = self.oai_client.images.generate(
                model = 'dall-e-3',
                prompt = prompt,
                n = 1,
                size = '1024x1024',
                quality = 'standard',
                style = 'natural'
            )
            image_url = response.data[0].url
            image_url_get = requests.get(image_url)

            img_uid = str(shortuuid.uuid())
            img_path = f'./tmp/conti/{ img_uid }.png'
            with open( img_path, 'wb' ) as f:
                f.write( image_url_get.content )
            
            if not load_conti:
                self.db.insert_conti( data, img_path, scenario_idx )
            else:
                self.db.update_conti( data, img_path, scenario_idx )
            
    def save_conti( self, scenario_idx ):
        wb = Workbook()
        ws = wb.active

        contis = self.db.load_conti( scenario_idx )

        for row, conti_data in enumerate( contis ):
            scene = conti_data[1]
            img_path = conti_data[2]

            cell = ws.cell( row = row+1, column = 1 , value = scene )
            cell.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')

            with open(img_path, 'rb') as img_file:
                img = Image(BytesIO(img_file.read()))
            img.height = 320
            img.width = 320
            ws.add_image( img, 'B{}'.format( row + 1 ) )
            ws.row_dimensions[ row+1 ].height = 320
            ws.column_dimensions[ 'A' ].width = 90

        conti_path = './tmp/conti.xlsx'
        wb.save(  conti_path )
        return conti_path
