from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Menu
import sys
import io
import cgi
from django.urls import reverse
from .forms import MenuForm



#ETC part
# 해본 음식은 색깔 바꾸게 하기. -> JS
# search keywords by tag key
# 모든 메뉴(All menu), 집밥 메뉴(home cook), 분위기 메뉴(Mood), 올킬 메뉴(Clearance)
# 배포

# 재료 입력 (고기 or 돼지고기)-> 동일검색결과. +면도 되게 하기. OK
# views.refactoring *띄어쓰기 상관없이 같은결과. OK
# db구현화(name클릭하면 필드 나오기) OK
# 나의 review & 댓글,후기, Q&A OK
# 이름 오류 바꾸기 OK
# 2가지 이상 재료 검색 & 검색창 설정하기 OK
# url field만들기 OK
# 없으면 출력 안시키기 OK
# CSS 꾸미기 (index.page, create page) OK
# db name 순서대로 OL

# nav var PP
# 양념들 어떻게 할지 -> model에서 non-essneitals재료 추가.PP



'''
고기 없을 때:
    - startswith
    - input1 == [q]:
        -save하고 원래꺼

고기 있을 때:
    - startswith
    - len == 1(고기)
    - 1 >:
        (-1)하고 원래꺼

'''
def test(request, food):
    menus = Menu.objects.all().order_by('name')
    food = Menu.objects.all().get(name=food)
    Essential_Ingredient = Menu.objects.values_list('Essential_Ingredient', flat=True).get(name=food) #모델에 있는 메뉴 재료
    Nonessential_Ingredient = Menu.objects.values_list('Nonessential_Ingredient', flat=True).get(name=food) #모델에 있는 메뉴 재료
    link = Menu.objects.values_list('link', flat=True).get(name=food) #모델에 있는 메뉴 재료
    tip = Menu.objects.values_list('tip', flat=True).get(name=food) #모델에 있는 메뉴 재료
    context = {'menus':menus, 'food' : food, 'Essential_Ingredient' : Essential_Ingredient, 'Nonessential_Ingredient':Nonessential_Ingredient,
    'link' : link, 'tip' : tip}
    return render(request, 'foodapp/test.html', context)

def index(request):
    menus = Menu.objects.all().order_by('name')
    names = list(Menu.objects.values_list('name', flat=True)) #모델에 있는 메뉴 #flat을 사용하면 tuple말고 리스트 형태로 가져올 수 있다.
    ingredients = list(Menu.objects.values_list('Essential_Ingredient', flat=True)) #모델에 있는 메뉴 재료
    nonessential_ingredients = list(Menu.objects.values_list('Nonessential_Ingredient', flat=True)) #모델에 있는 메뉴 재료
    len1 = len(names)
    len2 = len(ingredients)

    global ingredient_list
    global nonessential_ingredients_list
    ingredient_list = []
    nonessential_ingredients_list = []


    for food in ingredients: # ingredients_as_values = '마늘, 밥, 버터', '국, 밥' , food = '마늘, 밥, 버터'
        if food:
            vv = food.split(',') #food = '마늘, 밥, 버터' vv = ['마늘', ' 밥', '버터']
            ingredient_list.append(vv)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']
        else:
            ingredient_list.append(food)

    for i in nonessential_ingredients: # ingredients_as_values = '마늘, 밥, 버터', '국, 밥' , food = '마늘, 밥, 버터'
        if food:
            qq = i.split(',') #food = '마늘, 밥, 버터' vv = ['마늘', ' 밥', '버터']
            nonessential_ingredients_list.append(qq)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']
        else:
            nonessential_ingredients_list.append(i)

    context = {
    'menus':menus, 'names':names, 'nonessential_ingredients_list':nonessential_ingredients_list}
    return render(request, 'foodapp/index.html', context)

def search(request):
    menus = Menu.objects.all().order_by('name')
    names = list(Menu.objects.values_list('name', flat=True))
    ingredients = list(Menu.objects.values_list('Essential_Ingredient', flat=True))
    input = request.GET.get('food')
    split_my_input = input.split(', ')

    meat_including_menus = ((Menu.objects.filter(Essential_Ingredient__contains='베이컨')|Menu.objects.filter(Essential_Ingredient__contains='다진 돼지고기')
    |Menu.objects.filter(Essential_Ingredient__contains='고기')|Menu.objects.filter(Essential_Ingredient__contains='소고기')
    |Menu.objects.filter(Essential_Ingredient__contains='목살')|Menu.objects.filter(Essential_Ingredient__contains='대패삼겹살')
    |Menu.objects.filter(Essential_Ingredient__contains='앞다리살')|Menu.objects.filter(Essential_Ingredient__contains='양념돼지갈비')
    |Menu.objects.filter(Essential_Ingredient__contains='닭 다리살')))
    meat_including_menus_names = list(meat_including_menus.values_list('name',flat=True))
    meat_including_menus_ingredients = list(meat_including_menus.values_list('Essential_Ingredient',flat=True))

    noodle_including_menus = ((Menu.objects.filter(Essential_Ingredient__contains='면')
    |Menu.objects.filter(Essential_Ingredient__contains='라면')|Menu.objects.filter(Essential_Ingredient__contains='우동')
    |Menu.objects.filter(Essential_Ingredient__contains='칼국수')|Menu.objects.filter(Essential_Ingredient__contains='우동사리')
    |Menu.objects.filter(Essential_Ingredient__contains='쫄면')))
    noodle_including_menus_names = list(noodle_including_menus.values_list('name',flat=True))
    noodle_including_menus_ingredients = list(noodle_including_menus.values_list('Essential_Ingredient',flat=True))



    save_my_input = []
    menu_one, menu_two, menu_three, menu_four, menu_ETC = [], [], [], [], []
    menu_one_ingredient, menu_two_ingredient, menu_three_ingredient, menu_four_ingredient, ETC_ingredient = [], [], [], [], []
    new_ingredients_of_menu_list = []

    menu_list = (names)
    ingredients_of_menu_list = ingredient_list
    category_menu = ['고기', '면']

    if '고기' in input:
        menu_list = (meat_including_menus_names)
        ingredients_of_menu_list = meat_including_menus_ingredients
        for i in ingredients_of_menu_list:
            new_ingredients_of_menu_list.append(i.split(','))
        ingredients_of_menu_list = new_ingredients_of_menu_list #[['면', '마늘', '베이컨', '파마산치즈'], ['대파', '다진 돼지고기', '두부'], ['면', '소고기', '마늘'], ['목살', '파프리카', '감자', '당근', '양파', '카레 '], ['대패삼겹살', '양파', '양배추', '대파', '라면'], ['대패삼겹살', '마늘', '양배추', '대파'], ['시금치', '베이컨', '마늘'], ['감자', '양파', '당근', '양념돼지갈비', '케찹', '버터', '양배추', '간마늘', '간장'], ['당근', '청양고추', '감자', '양파', '닭 다리살', '대파', '양배추', '마늘', '우동사리', '떡사리'], ['감자', '베이컨'], ['두부', '계란', '대파', '양파', '다진 돼지고기', '청양고추'], ['부추', '면', '대패삼겹살'], ['앞다리살', '버섯', '파프리카'], ['면', '베이컨', '양배추'], ['버섯', '양파', '얇은 고기', '하이라이스'], ['육수', '양배추', '깻잎', '얇은 고기'], ['아스파라거스', '베이컨', '버터', '양파', '화이트와인']]

    if '면' in input:
        menu_list = (noodle_including_menus_names)
        ingredients_of_menu_list = noodle_including_menus_ingredients
        for i in ingredients_of_menu_list:
            new_ingredients_of_menu_list.append(i.split(','))
        ingredients_of_menu_list = new_ingredients_of_menu_list

    for iii in split_my_input: # if input1 == '고기': narrow down menu_list including '고기'. Then, when input1 == '면', narrow down menu_list again from previous menu_list.
        if iii in category_menu:
            menu_list = set(menu_list & iii)

    i = 0
    while (i < len(menu_list)):
        for input1 in split_my_input:
            q = 0
            while(q < len(ingredients_of_menu_list[i])):
                if (ingredients_of_menu_list[i])[q].startswith(' '):
                    (ingredients_of_menu_list[i])[q] = (ingredients_of_menu_list[i])[q][1:]

                if input1 in category_menu:
                    break

                if input1 == (ingredients_of_menu_list[i])[q]:
                    save_my_input.append(input1)

                q = q + 1

        length_variable = len(save_my_input) #면, 마늘
        for q in category_menu: #고기, 면
            if q in split_my_input:
                length_variable = length_variable + 1

        if len(split_my_input) == length_variable:
            if len(ingredients_of_menu_list[i]) == 1:
                menu_one.append(menu_list[i])
                menu_one_ingredient.append(', '.join(sorted(ingredients_of_menu_list[i])))

            elif len(ingredients_of_menu_list[i]) == 2:
                menu_two.append(menu_list[i])
                menu_two_ingredient.append(', '.join(sorted(ingredients_of_menu_list[i])))

            elif len(ingredients_of_menu_list[i]) == 3:
                menu_three.append(menu_list[i])
                menu_three_ingredient.append(', '.join(sorted(ingredients_of_menu_list[i])))

            elif len(ingredients_of_menu_list[i]) > 3:
                menu_four.append((menu_list[i]))
                menu_four_ingredient.append(', '.join(sorted(ingredients_of_menu_list[i])))

        save_my_input = []
        i = i + 1

    len_try_a, len_try_b, len_try_c, len_try_d = len(menu_one), len(menu_two), len(menu_three), len(menu_four)
    menu_set1, menu_set2, menu_set3, menu_set4 = {}, {}, {}, {}

    if menu_one:
        for qq in range(0, len(menu_one)):
            menu_set1[menu_one[qq]] = (menu_one_ingredient[qq])

    if menu_two:
        for qq in range(0, len(menu_two)):
            menu_set2[menu_two[qq]] = (menu_two_ingredient[qq])

    if menu_three:
        for qq in range(0, len(menu_three)):
            menu_set3[menu_three[qq]] = (menu_three_ingredient[qq])

    if menu_four:
        for qq in range(0, len(menu_four)):
            menu_set4[menu_four[qq]] = (menu_four_ingredient[qq])


    context = {'menu_ETC':menu_ETC, 'ETC_ingredient':ETC_ingredient, 'meat_including_menus_names' : meat_including_menus_names,
    'input' : input, 'menus' : menus, 'meat_including_menus' : meat_including_menus,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    'menu_one_ingredient' : menu_one_ingredient, 'menu_two_ingredient' : menu_two_ingredient, 'menu_three_ingredient' : menu_three_ingredient, 'menu_four_ingredient' :menu_four_ingredient,
    'menu_set1': menu_set1, 'menu_set2': menu_set2, 'menu_set3': menu_set3, 'menu_set4': menu_set4,
    'len_try_a' : len_try_a, 'len_try_b' : len_try_b, 'len_try_c' : len_try_c, 'len_try_d' : len_try_d
    }
    return render(request, 'foodapp/search.html', context)

def create(request):
    menus = Menu.objects.all().order_by('name')
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            obj = Menu(name=form.data['name'], Essential_Ingredient=form.data['Essential_Ingredient'], Nonessential_Ingredient=form.data['Nonessential_Ingredient'], link=form.data['link'], tip=form.data['tip'])
            obj.save()
            return redirect('http://127.0.0.1:8000/')
        return HttpResponse('fail')
    elif request.method == 'GET':
        form = MenuForm()
        return render(request, 'foodapp/create.html', {'form': form, 'menus' : menus})
    else:
        pass
