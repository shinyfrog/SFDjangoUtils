from django.db    import models

from sfModel      import SFModel


class SFModelOrdered(SFModel):

    order = models.PositiveIntegerField (db_index=True, default=1)

    def save(self):

        toOrder = False
        if not self.id:
            toOrder = True

        super(SFModelOrdered, self).save()

        if toOrder:
            try:
                self.order = self.__class__.orderingQuerySet()[0].order + 1
            except:
                pass

        super(SFModelOrdered, self).save()

    def changeOrder(self, newOrder):
        changeElementOrder(self, newOrder, self.orderingQuerySet())

    def orderingQuerySet(self):
        """
            Redefine this function if you want to implement
        """
        return self.__class__.objects.all()

    class Meta:
        abstract = True


def changeElementOrder(element, newOrder, elements):
    """
    This function reorder any objects list of django objects with a "order" attribute
    """

    firstIndex =  min(element.order, newOrder)
    lastIndex  = max(element.order, newOrder)

    down = False
    if(firstIndex == element.order):
        down = True

    if down:

        elements = elements.filter(order__gt=firstIndex, order__lte=lastIndex).order_by('order')
        counter = 0

        for c in elements:
            c.order = self.order + counter
            c.save()
            counter += 1

    else:

        elements = elements.filter(order__gte=firstIndex, order__lt=lastIndex).order_by('order')
        counter = 1

        for c in elements:
            c.order = firstIndex + counter
            c.save()
            counter += 1

    element.order = newOrder
    element.save()
