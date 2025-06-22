import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

print("모델 훈련을 시작합니다...")

# 1. 데이터 불러오기
# 데이터 파일들이 저장된 경로를 지정합니다.
data_path = 'data/'
try:
    df_train = pd.read_csv(os.path.join(data_path, 'train.txt'), sep=';', names=['text', 'label'])
    df_val = pd.read_csv(os.path.join(data_path, 'val.txt'), sep=';', names=['text', 'label'])
    df_test = pd.read_csv(os.path.join(data_path, 'test.txt'), sep=';', names=['text', 'label'])
    
    # train, validation, test 데이터를 모두 합쳐서 전체 데이터셋을 구성합니다.
    df = pd.concat([df_train, df_val, df_test], ignore_index=True)
    print(f"데이터 로드 완료. 전체 샘플 개수: {len(df)}")
    print("데이터셋 분포:\n", df['label'].value_counts())

except FileNotFoundError:
    print(f"오류: '{data_path}' 폴더에서 데이터 파일을 찾을 수 없습니다.")
    print("1단계 가이드에 따라 파일을 올바르게 위치시켰는지 확인해주세요.")
    exit()


# 2. 레이블을 숫자로 변환 (Label Encoding)
labels = df['label'].unique()
label_to_id = {label: i for i, label in enumerate(labels)}
id_to_label = {i: label for i, label in enumerate(labels)}
df['label_id'] = df['label'].map(label_to_id)

print("\n감정 레이블과 ID 매핑:")
print(id_to_label)

# 3. 훈련/테스트 데이터 분리 (전체 데이터를 다시 8:2로 나눔)
X = df['text']
y = df['label_id']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. 텍스트 벡터화 (TF-IDF)
print("\nTF-IDF 벡터화를 진행합니다...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
print("벡터화 완료.")

# 5. 모델 학습
print("\nRandom Forest 모델 학습을 시작합니다. (시간이 다소 걸릴 수 있습니다)...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train_vec, y_train)
print("모델 학습 완료.")

# 6. 모델 평가
print("\n모델 성능 평가:")
y_pred = model.predict(X_test_vec)
# target_names를 올바르게 전달하기 위해 id_to_label을 정렬하여 사용
target_names = [id_to_label[i] for i in sorted(id_to_label)]
print(classification_report(y_test, y_pred, target_names=target_names))

# 7. 새로운 모델과 관련 파일들을 'model' 폴더에 저장
model_dir = 'model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

with open(os.path.join(model_dir, "multiclass_model.pkl"), "wb") as f:
    pickle.dump(model, f)
with open(os.path.join(model_dir, "multiclass_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)
with open(os.path.join(model_dir, "id_to_label.pkl"), "wb") as f:
    pickle.dump(id_to_label, f)

print(f"\n✅ 새로운 모델과 파일들이 '{model_dir}' 폴더에 성공적으로 저장되었습니다!")