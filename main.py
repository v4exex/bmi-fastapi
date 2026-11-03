from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get("/bmi")
def input_bmi(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='bmi_input.html'
    )

@app.get("/bmi/print")
def print_bmi(request: Request, height: int, weight: int):
    result = compute_bmi(weight, height)
    return templates.TemplateResponse(
        request=request,
        name='bmi_result.html',
        context={ 'result': result }
    )

def compute_bmi(weight: int, height: int):
    bmi = round(weight / (height / 100) ** 2, 1)
    if bmi < 18.5:
        status, level = '저체중', 'low'
        message = '조금 더 챙겨 먹어도 좋아요. 균형 잡힌 식사와 근력 운동을 추천해요.'
    elif bmi < 23:
        status, level = '정상', 'normal'
        message = '아주 좋아요! 지금의 생활 습관을 유지하세요.'
    elif bmi < 25:
        status, level = '과체중', 'over'
        message = '조금만 신경 쓰면 돼요. 가벼운 유산소 운동을 시작해 보세요.'
    else:
        status, level = '비만', 'obese'
        message = '건강을 위해 식단과 운동 관리를 권해요. 걱정 말고 천천히 시작해요.'

    m = height / 100
    min_weight = round(18.5 * m ** 2, 1)  
    max_weight = round(22.9 * m ** 2, 1)  
    if weight < min_weight:
        diff = round(min_weight - weight, 1)    
    elif weight > max_weight:
        diff = round(max_weight - weight, 1)    
    else:
        diff = 0

    pos = round(min(max((bmi - 15) / 20, 0), 1) * 100, 1)

    return {
        'bmi': bmi,
        'status': status,
        'level': level,
        'message': message,
        'height': height,
        'weight': weight,
        'min_weight': min_weight,
        'max_weight': max_weight,
        'diff': diff,
        'pos': pos,
    }


