# from celery import shared_task
# from faker import Faker
# from .models import Product, Category
# import random


# class GenerateDummyDataView(FormView):
#     template_name = 'product/generate_dummy_data.html'
#     form_class = DummyDataForm
#     success_url = '/path-to-redirect-after-success/'  # Set this to your desired URL

#     def form_valid(self, form):
#         fake = Faker()
#         num_products = form.cleaned_data['num_products']

#         categories = Category.objects.all()
#         if not categories.exists():
#             for _ in range(5):
#                 Category.objects.create(name=fake.word())

#         for _ in range(num_products):
#             category = random.choice(categories)
#             Product.objects.create(
#                 category=category,
#                 title=fake.catch_phrase(),
#                 description=fake.text(),
#                 price=round(random.uniform(10.0, 1000.0), 2),
#                 status='Pending'
#             )
        
#         # Add a success message or any other context data if needed
#         return super().form_valid(form)
