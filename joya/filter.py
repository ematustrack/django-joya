 from django.contrib.admin.filters import AllValuesFieldListFilter

class DropdownFilter(AllValuesFieldListFilter):
    template = 'dropdown_filter.html'