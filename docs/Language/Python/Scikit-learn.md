# Scikit-learn 语法笔记
## 1. 基本概念
### 什么是 Scikit-learn？
**Scikit-learn（简称 sklearn）** 是 Python 最主流的机器学习库，建立在 NumPy、SciPy 和 Matplotlib 之上，提供：
- 统一的 API 接口
- 丰富的监督/无监督学习算法
- 模型评估、数据预处理、特征工程、模型选择等完整工具链
**核心设计哲学：**
- 一致性：所有模型都遵循 `fit()`, `predict()`, `transform()` 等统一接口
- 可组合性：Pipeline、FeatureUnion 等支持模块化组合
- 文档完善、社区活跃、工业级稳定
## 2. 核心模块概览
```python
from sklearn import datasets        # 内置数据集
from sklearn import model_selection # 数据划分、交叉验证
from sklearn import preprocessing   # 数据预处理
from sklearn import feature_selection # 特征选择
from sklearn import decomposition   # 降维
from sklearn import pipeline        # 管道
from sklearn import metrics         # 评估指标
from sklearn import ensemble        # 集成方法
from sklearn import linear_model    # 线性模型
from sklearn import svm             # 支持向量机
from sklearn import neighbors       # KNN
from sklearn import tree            # 决策树
from sklearn import cluster         # 聚类
```
## 3. 数据准备与划分
### 内置数据集
```python
from sklearn.datasets import load_iris, load_boston, load_digits

iris = load_iris()
X, y = iris.data, iris.target  # (150, 4), (150,)
digits = load_digits()
print(digits.images.shape)     # (1797, 8, 8) → 可展平为 (1797, 64)
```
### 数据划分（训练集/测试集）
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 测试集占比
    random_state=42,    # 随机种子，保证可复现
    stratify=y          # 分层抽样（分类任务推荐）
)
```
### 交叉验证
```python
from sklearn.model_selection import cross_val_score, KFold

scores = cross_val_score(model, X, y, cv=5)  # 5折交叉验证
print("CV Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# 自定义折数
kf = KFold(n_splits=5, shuffle=True, random_state=42)
```
## 4. 数据预处理（Preprocessing）
### 标准化（StandardScaler）
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 拟合+转换
X_test_scaled = scaler.transform(X_test)        # 仅转换（使用训练集参数）
```
### 归一化（MinMaxScaler）
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)
```
### 编码分类变量
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

# LabelEncoder：字符串 → 整数
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# OneHotEncoder：整数 → 独热编码
ohe = OneHotEncoder(sparse_output=False)  # 返回数组而非稀疏矩阵
X_cat_encoded = ohe.fit_transform(X_cat.reshape(-1, 1))

# 混合数值+分类列处理
ct = ColumnTransformer([
    ('num', StandardScaler(), [0,1,2]),
    ('cat', OneHotEncoder(), [3,4])
])
X_processed = ct.fit_transform(X)
```
### 缺失值填充
```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')  # 或 'median', 'most_frequent', 'constant'
X_imputed = imputer.fit_transform(X)
```
## 5. 特征工程与降维
### 特征选择
```python
from sklearn.feature_selection import SelectKBest, f_classif, RFE

# 基于统计检验（如ANOVA F值）
selector = SelectKBest(score_func=f_classif, k=3)
X_selected = selector.fit_transform(X, y)

# 递归特征消除（RFE）
from sklearn.linear_model import LogisticRegression
estimator = LogisticRegression()
rfe = RFE(estimator, n_features_to_select=3)
X_rfe = rfe.fit_transform(X, y)
```
### 降维（PCA / t-SNE）
```python
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# PCA
pca = PCA(n_components=2)  # 或 n_components=0.95 保留95%方差
X_pca = pca.fit_transform(X)

# t-SNE（适合可视化）
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X)
```
## 6. 常用模型速查
### 分类模型
```python
# 逻辑回归
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

# 支持向量机
from sklearn.svm import SVC
svm = SVC(kernel='rbf', C=1.0)

# K近邻
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5)

# 决策树
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(max_depth=5)

# 随机森林（集成）
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100)

# 梯度提升树
from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier()
```
### 回归模型
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

lr = LinearRegression()
ridge = Ridge(alpha=1.0)
lasso = Lasso(alpha=0.1)
svr = SVR(kernel='rbf')
rf_reg = RandomForestRegressor()
```
### 无监督学习（聚类）
```python
from sklearn.cluster import KMeans, DBSCAN

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X)
```
## 7. 模型训练与预测
### 统一接口：
```python
model = LogisticRegression()
model.fit(X_train, y_train)          # 训练
y_pred = model.predict(X_test)       # 预测类别
y_proba = model.predict_proba(X_test) # 预测概率（分类）
y_pred = model.predict(X_test)       # 预测值（回归）
```
### 多分类支持：
- Sklearn 默认支持 **OvR（One-vs-Rest）** 和 **Multinomial**
- SVC 需设置 `decision_function_shape='ovr'` 或 `'ovo'`
## 8. 模型评估
### 分类评估指标
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='macro')  # micro / macro / weighted
rec = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# AUC（仅适用于二分类或 OvR 多分类）
auc = roc_auc_score(y_test, y_proba[:, 1])  # 二分类取正类概率
```
### 回归评估指标
```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```
### 绘制 ROC 曲线（二分类）
```python
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_test, y_proba[:, 1])
plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % auc)
plt.plot([0,1], [0,1], 'k--')  # 对角线
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
```
## 9. 模型调优（超参数搜索）
### 网格搜索（GridSearchCV）
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto', 0.001, 0.01]
}

svm = SVC()
grid = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)
print("Best score:", grid.best_score_)
best_model = grid.best_estimator_
```
### 随机搜索（RandomizedSearchCV）
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

param_dist = {
    'C': uniform(0.1, 10),          # 连续均匀分布
    'gamma': ['scale', 'auto'] + list(np.logspace(-3, 1, 10)),
    'max_depth': randint(3, 10)     # 整数离散分布
}

rf = RandomForestClassifier()
random_search = RandomizedSearchCV(rf, param_dist, n_iter=20, cv=5, random_state=42)
random_search.fit(X_train, y_train)
```
## 10. 管道（Pipeline）
将预处理、特征选择、模型训练串联，避免数据泄露，提升可维护性。
```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=5)),
    ('classifier', LogisticRegression())
])

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

# 与 GridSearch 结合
param_grid = {
    'pca__n_components': [2, 5, 10],
    'classifier__C': [0.1, 1, 10]
}

grid = GridSearchCV(pipe, param_grid, cv=5)
grid.fit(X_train, y_train)
```
## 11. 实用技巧 & 注意事项
### 数据泄露（Data Leakage）
- **错误做法**：在 `train_test_split` 前做标准化或填充缺失值
- **正确做法**：只在训练集上 `fit`，然后 `transform` 测试集 → **使用 Pipeline 最安全**
### 保存与加载模型
```python
import joblib  # sklearn 推荐使用 joblib，比 pickle 更高效

joblib.dump(model, 'model.pkl')
loaded_model = joblib.load('model.pkl')
```
### 可视化决策树
```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plot_tree(dt, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)
plt.show()
```
### 自定义评估指标
```python
from sklearn.metrics import make_scorer

def custom_metric(y_true, y_pred):
    return np.mean(y_true == y_pred)  # 示例：准确率

custom_scorer = make_scorer(custom_metric, greater_is_better=True)
grid = GridSearchCV(model, param_grid, scoring=custom_scorer)
```
### 多输出 / 多标签分类
```python
from sklearn.multioutput import MultiOutputClassifier

# 一个样本多个标签（如：图像同时有“猫”和“户外”标签）
multi_target_model = MultiOutputClassifier(RandomForestClassifier())
multi_target_model.fit(X_train, y_train_multi)  # y_train_multi shape: (n_samples, n_labels)
```

## 附录：常用缩写与术语

| 缩写 | 全称 | 说明 |
|------|------|------|
| CV | Cross Validation | 交叉验证 |
| OvR | One-vs-Rest | 一对多策略 |
| OvO | One-vs-One | 一对一策略 |
| PCA | Principal Component Analysis | 主成分分析 |
| RFE | Recursive Feature Elimination | 递归特征消除 |
| AUC | Area Under Curve | ROC 曲线下面积 |
| MSE | Mean Squared Error | 均方误差 |
| MAE | Mean Absolute Error | 平均绝对误差 |
| R² | R-squared | 决定系数 |
