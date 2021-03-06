import math, pandas, re, copy

with open("Jason Schreier.txt", 'rb') as file: Text = file.read().decode('utf-8') # jason schreier.txt -> something.txt

pattern_1 = r'ё'
pattern_2 = r'ъ'    
pattern_3 = r'[^абвгдежзийклмнопрстуфхцчшщыьэюя ]'

Text = re.sub(pattern_1, 'е', Text.lower())
Text = re.sub(pattern_2, 'ь', Text)
Text = re.sub(pattern_3, '', Text) 
Text_with_space = Text
Text = list(''.join(Text.split()))

rus_with_space = 'абвгдежзийклмнопрстуфхцчшщыьэюя '
rus_no_space = 'абвгдежзийклмнопрстуфхцчшщыьэюя'

alphabet_no_space = dict.fromkeys(list(rus_no_space), 0)
alphabet_with_space = dict.fromkeys(list(rus_with_space), 0) 


#Подсчет букв в тексте
for i in Text_with_space:alphabet[i] += 1
for i in Text: alphabet_no_space[i] += 1

def dictionary_sorting(dictionary):
    values = sum(dictionary.values())
    frequency = [(i, round(dictionary[i]/values, 7)) for i in sorted(dictionary.keys(), key=dictionary.get, reverse=True)]
    H_entropy = [(i, -dictionary[i]/values*math.log(dictionary[i] / values, 2)) for i in sorted(dictionary.keys(), key=dictionary.get, reverse=True)]
    
    return frequency, H_entropy

print('_______________________________________________________________________')
print('Частота букв текста: ', dictionary_sorting(alphabet_with_space)[0])
print('_______________________________________________________________________')
print('Энтропия букв текста: ', dictionary_sorting(alphabet_with_space)[1])
print('_______________________________________________________________________')
print('Энтропия букв текста без пробелов: ', dictionary_sorting(alphabet_no_space)[1])


#Инициализация датафрейма
data_no_spaces = pandas.DataFrame(columns = list(rus_no_space), index = list(rus_no_space), data = 0.0)
data_with_spaces = pandas.DataFrame(columns = list(rus_with_space), index = list(rus_with_space), data = 0.0)

#Запись данных из словаря с биграммами в датафрейм
def matrix(data, dict_):
    values = sum(dict_.values())
    data_H_entropy = copy.deepcopy(data)
    
    for i in dict_.keys(): 
        data[i[1]][i[0]] = dict_[i]/values
        data_H_entropy[i[1]][i[0]] = -dict_[i]/values*math.log(dict_[i]/values, 2)
        
    return data, data_H_entropy

#Считываем текст, подсчёт количества биграмм и запись их в словарь
    
#Непересекающиеся биграммы
def disjoint_bigrams(Text):
    bigram = {}
    
    for i in range(math.ceil((len(Text) - 1) / 2)):
        if ''.join(Text[2*i: 2*i+2]) in bigram:
            bigram[''.join(Text[2*i: 2*i+2])] += 1
        else:
            bigram[''.join(Text[2*i: 2*i+2])] = 1
            
    return bigram   
 
#Пересекающиеся биграммы
def intersecting_bigrams(Text):
    bigram = {}
    
    for i in range(len(Text) - 1):
        if ''.join(Text[i: i+2]) in bigram:
            bigram[''.join(Text[i: i+2])] += 1
        else:
            bigram[''.join(Text[i: i+2])] = 1
            
    return bigram


#Запись пересекающихся и непересекающихся биграмм и их энтропиями текста с пробеламы в Excel
array_for_intersecting_bigrams = matrix(data_with_spaces, intersecting_bigrams(Text_with_space)) 
array_for_disjoint_bigrams = matrix(data_with_spaces, disjoint_bigrams(Text_with_space))

array_for_intersecting_bigrams[0].to_excel('Частоты пересекающихся биграмм с пробелами.xlsx')
array_for_disjoint_bigrams[0].to_excel('Частоты непересекающихся биграмм с пробелами.xlsx')
array_for_intersecting_bigrams[1].to_excel('Энтропия пересекающихся биграмм с пробелами.xlsx')
array_for_disjoint_bigrams[1].to_excel('Энтропия непересекающихся биграмм с пробелами.xlsx')

#Запись пересекающихся и непересекающихся биграмм и их энтропиями в Excel
matrix(data_no_spaces, intersecting_bigrams(Text))[1].to_excel('Энтропия пересекающихся биграмм без пробелов.xlsx')
matrix(data_no_spaces, disjoint_bigrams(Text))[1].to_excel('Энтропия непересекающихся биграмм без пробелов.xlsx')
