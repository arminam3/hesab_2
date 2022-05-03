from django.shortcuts import render, reverse ,get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from .forms import CreateMoneyForm, CreateShoppingForm
from .models import Week, Shopping, Money, Hesab, MainHesab, LastHesab



class WeekList(generic.ListView):
    model = Week
    template_name = 'hesab/week_list.html'
    context_object_name = 'week_list'


def refresh(request, pk):
    week = Week.objects.get(id=pk)
    all_money = Money.objects.filter(week=week).order_by('-money')
    shopping = Shopping.objects.filter(week=week).order_by('name')
    moneys = Money.objects.filter(week=week)
    chosen_shopping = Shopping.objects.filter(week=week)
    m = 0
    for money in moneys:
        m+=1
        my_money = 0
        chosen_shopping_buyer = Shopping.objects.filter(week=week, buyer=money.user)

        for shop in chosen_shopping_buyer:
            my_money += int(shop.amount)
        for shop in chosen_shopping:
            numbers = shop.consumer.all().count()
            if money.user in shop.consumer.all():
                my_money -= int(shop.amount / numbers)
            Money.objects.filter(user=money.user, week=week).update(money=my_money)
    sum = 0
    for s in shopping:
        sum += s.amount
    Week.objects.filter(id=pk).update(sum=sum)
    try:
        return render(request, 'hesab/week_details.html', {'week': week, 'sum': week.sum, 'shopping': shopping,'all_money':all_money})

    except:
        return render(request, 'hesab/week_details.html', {'week': week, 'sum': week.sum, 'shopping': shopping})

def week_details(request, pk):
    week = Week.objects.get(id=pk)
    all_money = Money.objects.filter(week=week).order_by('-money')
    shopping = Shopping.objects.filter(week=week).order_by('name')

    week_money = 0
    context = {
        'week': week,
        'sum': week.sum,
        'shopping': shopping,
        'all_money': all_money
    }
    return render(request, 'hesab/week_details.html', context)


def money_create_view(request, pk):
    week = Week.objects.get(id=pk)
    if request.method == 'POST':
        money_form = CreateMoneyForm(request.POST)
        if money_form.is_valid():
            for n in money_form.cleaned_data['consumer']:
                money = Money(user=n, week=week)
                money.save()
            return HttpResponseRedirect(f'/{pk}/refresh/')

    else:
        money_form = CreateMoneyForm()
        context = {
            'form': money_form
        }
        return render(request, 'hesab/create_money.html',context )

def shopping_create_view(request, pk):
    week = Week.objects.get(id=pk)
    week_sum = week.sum
    if request.method == 'POST':
        shop_form = CreateShoppingForm(request.POST)
        if shop_form.is_valid():
            shop = Shopping.objects.create(
                             week=week,
                             name=shop_form.cleaned_data['name'],
                             goods=shop_form.cleaned_data['goods'],
                             buyer=shop_form.cleaned_data['buyer'],
                             amount=shop_form.cleaned_data['amount'],
                             )
            # shop.save()
            if shop_form.cleaned_data['consumer']:
                for n in shop_form.cleaned_data['consumer']:
                    shop.consumer.add(n)
            else:
                shop.delete()
                return HttpResponse('حداقل یک مصرف کننده تعریف کنید')
            numbers = shop.consumer.all().count()
            week_sum += shop.amount
            for con in shop.consumer.all():
                try:
                    money = Money.objects.get(week=week, user=con)
                    my_money = money.money
                    my_money -= int(shop.amount / numbers)
                except:
                    money = Money.objects.create(week=week, user=con, money=0)
                    my_money = money.money
                    my_money -= int(shop.amount / numbers)
                # print('-----')
                # if con.id == shop.buyer.id:
                #     print(my_money)
                #     my_money += shop.amount
                #     print(my_money)
                # else:
                bm = Money.objects.get(week=week,user=shop.buyer)
                bm_money = bm.money
                bm_money += shop.amount
                Money.objects.filter(week=week, user=shop.buyer).update(money=bm_money)
                Money.objects.filter(user=money.user, week=week).update(money=my_money)
            Week.objects.filter(id=pk).update(sum=week_sum)
            return HttpResponseRedirect(f'/{pk}/createshopping/')
        else:
            return HttpResponse('حداقل یک مورد را برای مصرف کنندگان انتخاب کنید !')

    else:
        shop_form = CreateShoppingForm()
        context = {
            'form': shop_form,
            "week": week
        }
        return render(request, 'hesab/create_shopping.html',context )




def hesab(request, pk):
    week = Week.objects.get(id=pk)
    shopping = Shopping.objects.filter(week=week).order_by('name')
    hesabs = Hesab.objects.filter(week=week).delete()
    for shop in shopping:
        for con in shop.consumer.all():
            if con != shop.buyer:
                Hesab.objects.create(plus=shop.buyer, negative=con, amount=shop.amount/shop.consumer.all().count(), week=week)
    hesabs = Hesab.objects.filter(week=week)
    print(hesabs)
    for hesab in hesabs:
        money = 0
        chosen_hesab = Hesab.objects.filter(week=week, plus=hesab.plus, negative=hesab.negative)
        for hesab2 in chosen_hesab:
            money += hesab.amount
            try:
                hesab_2 = MainHesab.objects.get(week=week, plus=hesab.plus, negative=hesab.negative)
                hesab_2.amount = money
            except:
                hesab_2 = MainHesab.objects.create(week=week, plus=hesab.plus, negative=hesab.negative, amount=money)
        chosen_hesab_2 = Hesab.objects.filter(week=week, plus=hesab.negative, negative=hesab.plus)
        for hesab2 in chosen_hesab_2:
            money -= hesab.amount
        try:
            hesab_2 = MainHesab.objects.get(week=week, plus=hesab.plus, negative=hesab.negative)
            hesab_2.amount = money
        except:
            hesab_2 = MainHesab.objects.create(week=week, plus=hesab.plus, negative=hesab.negative,amount=money)

    chosen_main_hesab = MainHesab.objects.filter(week=week)
    for main_hesab in chosen_main_hesab:
        main_hesab_p = MainHesab.objects.filter(week_id=pk, plus=main_hesab.plus,  negative=main_hesab.negative)
        for p in main_hesab_p:
            try:
                last = LastHesab.objects.get(week_id=pk, plus=main_hesab.plus,  negative=main_hesab.negative)
                last.money += p.amount
            except:
                last = LastHesab.objects.create(week_id=pk, plus=main_hesab.plus,  negative=main_hesab.negative, amount=p.amount)
        main_hesab_n = MainHesab.objects.filter(week_id=pk, plus=main_hesab.negative,  negative=main_hesab.plus)
        for n in main_hesab_n:
            try:
                last = LastHesab.objects.get(week_id=pk, plus=main_hesab.plus, negative=main_hesab.negative)
                last.money -= p.amount
            except:
                last = LastHesab.objects.create(week_id=pk, plus=main_hesab.plus, negative=main_hesab.negative,
                                             amount=-1*(p.amount))

    last_hesab = LastHesab.objects.filter(week=week)
    return render(request, 'hesab/all_hesab.html', {'hesabs': last_hesab})


def correct_hesab(request, pk):
    for h in Hesab.objects.all(): #حذف تمامی حساب ها
        h.delete()
    all_pos_money = Money.objects.filter(week_id=pk, money__gte=1).order_by('-money')
    all_neg_money = Money.objects.filter(week_id=pk, money__lte=-1).order_by('money')
    indent = 0
    pm_z = 0
    for neg_money in all_neg_money:
        nm = neg_money.money
        while 0 > nm:
            try:
                if not pm_z:
                    pos_money = all_pos_money[indent]
                    pm = pos_money.money
                else:
                    pos_money = all_pos_money[indent]
                    pm = pm_z

            except:
                break

            while pm> 0 > nm:
                if pm > -1 * nm:
                    Hesab.objects.create(week_id=pk, plus=pos_money.user, negative=neg_money.user, money=-1*nm)
                    pm += nm
                    nm = 0
                    pm_z = pm
                elif pm < -1 * nm:
                    Hesab.objects.create(week_id=pk, plus=pos_money.user, negative=neg_money.user, money=pm)
                    nm += pm
                    pm = 0
                    pm_z = 0
                    indent += 1
                else:
                    Hesab.objects.create(week_id=pk, plus=pos_money.user, negative=neg_money.user, money=pm)
                    nm = 0
                    pm = 0
                    pm_z = 0
                    indent += 1
    chosen_money = Money.objects.filter(week_id=pk).order_by('-money')
    chosen_hesab = Hesab.objects.filter(week_id=pk)
    context = {
        'all_money': chosen_money,
        'all_hesab': chosen_hesab,
    }
    return render(request, 'hesab/last_hesab.html',context)



class CreateWeek(generic.CreateView):
    model = Week
    template_name = 'hesab/create_money.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('week_details', args=[self.object.pk])

class DeleteWeek(generic.DeleteView):
    model = Week
    template_name = 'hesab/delete_week.html'
    success_url = reverse_lazy('week_list')




class DeleteMoney(generic.DeleteView):
    model = Money
    template_name = 'hesab/delete_week.html'

    def get_success_url(self):
        return f'/{self.object.week.id}/weekdetails/'

class DeleteShopping(generic.DeleteView):
    model = Shopping
    template_name = "hesab/delete_shopping.html"

    def get_success_url(self):
        return reverse('week_details', args=[self.object.week.id])

