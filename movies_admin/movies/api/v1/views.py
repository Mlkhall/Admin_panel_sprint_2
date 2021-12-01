from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from ...models import Filmwork

COUNT_OF_PAGE = 50


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        current_fields = ('id',
                          'title',
                          'description',
                          'creation_date',
                          'rating',
                          'type'
                          )

        return (Filmwork
                .objects
                .prefetch_related('genre', 'person')
                .values(*current_fields)
                .annotate(genres=ArrayAgg('genres__name',
                                          distinct=True),
                          actors=ArrayAgg('person__full_name',
                                          filter=Q(personfilmwork__role="actor"),
                                          distinct=True),
                          directors=ArrayAgg('person__full_name',
                                             filter=Q(personfilmwork__role="director"),
                                             distinct=True),
                          writers=ArrayAgg('person__full_name',
                                           filter=Q(personfilmwork__role="writer"),
                                           distinct=True)
                          )
                )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class Movies(MoviesApiMixin, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):

        paginator = Paginator(self.get_queryset(), COUNT_OF_PAGE)

        try:
            number_page = int(self.request.GET.get('page', None))
        except ValueError:
            if self.request.GET.get('page', None) == 'last':
                number_page = paginator.num_pages
            else:
                return {'result': 'Bad page'}
        except TypeError:
            number_page = 1

        number_page = 1 if number_page <= 0 else number_page

        current_page = paginator.page(number_page)
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": number_page - 1 if current_page.has_previous() else None,
            "next": number_page + 1 if current_page.has_next() else None,
            "results": list(current_page.object_list)
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return kwargs['object']
