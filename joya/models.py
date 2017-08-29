# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.utils.html import *
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg

# Create your models here.
Owner_type = (
    ('0', 'Feña'),
    ('1', 'Feña-Eduardo'),    
)

class TotalRow(ChangeList):
	fields_to_total = ['cost_price', 'profit',]

	def get_total_values(self, queryset):
		total = Sales()
		total.custom_alias_name = 'Total'
		for field in self.fields_to_total:
			setattr(total, field, queryset.aggregate(Sum(field)).items()[0][1])
		return total

	def get_results(self, request):
		super(TotalRow, self).get_results(request)
		total = self.get_total_values(self.queryset)
		len(self.result_list)
		self.result_list._result_cache.append(total)

class Supplier(models.Model):
	name = models.CharField('Nombre', max_length=200)
	email = models.EmailField('email', blank=True, null=True)
	phone = models.CharField('Telefono', max_length=200, blank=True, null=True)
	website = models.CharField('WebSite', max_length=200, blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Proveedor'

class Category(models.Model):
	name = models.CharField('Nombre', max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Categoria'
		


class Items(models.Model):
	category = models.ForeignKey(Category)
	supplier = models.ForeignKey(Supplier, null=True)
	code = models.CharField('Codigo', max_length=100)
	picture = models.ImageField(upload_to='media/pic_folder/')
	quantity = models.PositiveIntegerField('Cantidad')
	size = models.CharField('Talla', max_length=200, blank=True, null=True)
	notes = models.TextField('Descripcion', null=True, blank=True)
	cost_price = models.PositiveIntegerField('Costo')
	owner = models.CharField(max_length=20, choices=Owner_type, default='Feña-Eduardo')
	provider_code = models.CharField('Codigo proveedor', max_length=100, default='', null=True, blank=True)
	sell_price = models.PositiveIntegerField('Venta', default=0, null=True, blank=True)
	status = models.BooleanField('Activo', default=True)
	picture_thumbnail = ImageSpecField(source='picture',
                                      processors=[ResizeToFill(150, 150)],
                                      format='JPEG',
                                      options={'quality': 90})

	class Meta:
		verbose_name = 'Inventario'
		verbose_name_plural = 'Inventario'

	def __unicode__(self):
		return '%s' % self.code

	def image_img(self):
		if self.picture_thumbnail:
			return mark_safe('<img src="%s" />' % self.picture_thumbnail.url)

	def size_list(self):
		s = '<ul>'
		for i in self.size.split(','):
			talla, qty = i.split(':')
			s += '<li>Talla:%s Cantidad:%s</li>' % (talla, qty)
		s += '</ul>'
		return mark_safe(s)

	def image_drop(self):
		if self.picture_thumbnail:
			return mark_safe('<img src="%s" />' % self.picture_thumbnail.url)

	# def image_tag(self):
	# return mark_safe('<img src="/pic_folder/%s" width="150" height="150" />'
	# % (self.picture))

	# image_tag.short_description = 'Image'


class Sales(models.Model):
	item = models.ForeignKey(Items)
	qty = models.PositiveIntegerField('Cantidad')
	date = models.DateField(auto_now_add=True)
	price = models.PositiveIntegerField('Precio Venta')
	size = models.CharField('Tallas', max_length=200, blank=True, null=True)
	cost_price = models.PositiveIntegerField(default=0)
	profit = models.PositiveIntegerField(default=0)	
	note = models.TextField('Nota', default='', null=True, blank=True)

    #price = models.PositiveIntegerField('Precio Venta')
		
    
	def __unicode__(self):
		return ''

	class Meta:
		verbose_name = 'Venta'

class ItemsAdmin(admin.ModelAdmin):
	list_display = ('image_img', 'category', 'code', 'provider_code', 'notes', 'cost_price', 'sell_price', 'quantity', 'size_list', 'insert_sale',)
	list_filter = ('category',)
	search_fields = ['code']

	def insert_sale(self, obj):
		return mark_safe('<a href="/admin/joya/sales/add/?item=%s">Ingresar Venta</a>' % obj.id)

	def save_model(self, request, obj, form, change):
		obj.size = ''.join(obj.size.split())
		super(ItemsAdmin, self).save_model(request, obj, form, change)

class ItemsClient(Items):
	class Meta:
		proxy = True
		verbose_name = 'Inventario Clientes'

class ItemsClientAdmin(ItemsAdmin):
	list_display = ('image_img', 'category', 'code', 'sell_price', 'notes', 'quantity', 'insert_sale', )

	

class SalesAdmin(admin.ModelAdmin):
	list_display = ('get_item_code', 'get_image', 'qty', 'price', 'get_item_cost', 'get_individual_profit', 'get_total_profit', 'note',)
	list_filter = ('item', 'item__category',)
	search_fields = ['note']
	exclude = ('cost',)

	def get_form(self, request, obj=None, **kwargs):
		self.exclude = ('cost', 'profit', 'cost_price',)
		form = super(SalesAdmin, self).get_form(request, obj, **kwargs)
		return form

	def get_item_venta(self, obj):
		print obj.price
		return "${:,}".format(obj.profit)
	get_item_venta.short_description = 'Venta'

	def get_item_cost(self, obj):
		print obj.cost_price
		return "${:,}".format(obj.cost_price)
	get_item_cost.short_description = 'Costo'

	def get_item_category(self, obj):
		return obj.item.code

	def get_changelist(self, request, **kwargs):
		return TotalRow

	def get_item_code(self, obj):
		return obj.item.code

	def get_image(self, obj):
		return obj.item.image_img()

	def get_individual_profit(self, obj):
		return "${:,}".format(obj.profit) #(obj.price - obj.item.cost_price)
	get_individual_profit.short_description = 'Ganancia'

	def get_total_profit(self, obj):
		return "${:,}".format(obj.profit)
	get_total_profit.short_description = 'Ganancia Total'

	def save_model(self, request, obj, form, change):
		obj.cost_price = obj.item.cost_price
		print 'profit', obj.price, obj.item.cost_price, obj.qty
		obj.profit = (obj.price - obj.item.cost_price) * obj.qty
		try:
			if obj.item.category.id == 1 and len(obj.size) != 0:
				x = obj.size.split(',')
				t = obj.item.size.split(',')			
				for i in x:
					talla, cantidad = i.strip().split(':')
					for place, ii in enumerate(t):
						talla_s, cantidad_s = ii.strip().split(':')
						if talla == talla_s:
							t[place] = talla_s + ':' + str((int(cantidad_s)-int(cantidad)))
			obj.item.size = ','.join(t)
			
		except:
			pass
		obj.item.save()
		print obj.profit			
		super(SalesAdmin, self).save_model(request, obj, form, change)
		#obj.save()

	




admin.site.register(Category)
admin.site.register(Items, ItemsAdmin)
admin.site.register(ItemsClient, ItemsClientAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(Supplier)
