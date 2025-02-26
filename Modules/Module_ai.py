from Modules.Module_Basic import *
from Utils.Util_Env import get_env

envValue = get_env()

# MobileNetV2 모델 불러오기 (pretrained)
model = tf.keras.applications.MobileNetV2(weights="./datas/Ai_Models/mobilenet_v2_weights.h5")


def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.resize((224, 224))  # MobileNetV2 입력 크기에 맞게 조정
    image = np.array(image)
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    image = np.expand_dims(image, axis=0)  # 배치 차원 추가
    return image


def is_tumbler_or_bottle(predictions) -> dict:
    labels = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)
    for _, label, score in labels[0]:
        if "bottle" in label or "cup" in label:
            return {"result": True, "label": label, "confidence": round(score * 100, 2)}

    return {"result": False, "label": None, "confidence": None}


def get_model():
    model = SentenceTransformer("jhgan/ko-sroberta-multitask")
    return model


def get_dataset():
    df = pd.read_csv("datas/data_set.csv")
    df["embedding"] = df["embedding"].apply(json.loads)
    return df


def get_openai_options():
    openai_model = "text-davinci-003"
    openai_temperature = "0.5"
    openai_max_token = "2048"

    args = {
        "model": openai_model,
        "temperature": openai_temperature,
        "max_token": openai_max_token,
    }

    return args


def load_env():
    # openai에서 제공하는 API 값
    openai_token = envValue.get("OPENAI_TOKEN")

    # openai에 키 값을 로드
    openai.api_key = openai_token


def answer_from_chatgpt(query):
    answer = ""
    if query is None or len(query) < 1:
        answer = "글자 수 또는 질문이 없습니다."
        return answer

    options = get_openai_options()
    response = openai.Completion.create(
        model=options["model"],
        prompt=query,
        temperature=float(options["temperature"]),
        max_tokens=int(options["max_token"]),
    )
    res = response["choices"][0]["text"]
    answer = res

    return answer
