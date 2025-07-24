# Insights Data

## EDA 1 (Before preprocessing)

The dataset contains the following relevant features:

### Categorical data

#### Academic_Level
- Undergraduate: 353 samples
- Graduate: 325 samples
- High School: 27 samples

**Preprocessing decision:**  
Given the relatively small number of samples in the "High School" category compared to the others, and based on domain knowledge, I will assume that the academic level does not have a significant nonlinear effect on the target variable (social media addiction score). Therefore, I will apply **ordinal encoding** to this column as follows:

- High School = 0  
- Undergraduate = 1  
- Graduate = 2  

This encoding preserves the natural order of education levels while keeping the model simple.

#### Most_Used_Platform

- Facebook     123
- Instagram    249
- KakaoTalk     12
- LINE          12
- LinkedIn      21
- Snapchat      13
- TikTok       154
- Twitter       30
- VKontakte     12
- WeChat        15
- WhatsApp      54
- YouTube       10

**Preprocessing decision:**  
Given the many platforms with small amount of sample, I will group the platforms that are less than 5% of the total in to the same group 'other'

#### Relationship_Status

- Complicated         32
- In Relationship    289
- Single             384

### Textual data

**Preprocessing decision:**  
One hot encoding

#### Country

There are 110 different countries in the dataset. Many of them have only 1 occurence.

**Preprocessing decision:**  
Given the many different countires with one sample, I will try to group them by continent.

### Numerical data

**Preprocessing decision:**  
I will standardize all numerical data.

### Feature correlations

#### Age and the rest

It seems that there is no clear pattern between age and any of the other features. 

**Preprocessing decision:** 
I will keep the age feature for now and later in the project I will train the model without age column

**Note:** These assumptions will be revisited if later analyses or model interpretability results suggest otherwise.
