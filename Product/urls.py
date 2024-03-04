from django.urls import path
from .import views

urlpatterns = [
    path("MerchantProduct",views.MerchantProduct,name="MerchantProduct"),
    path("ProductsingleView/<int:pk>",views.ProductsingleView,name="ProductsingleView"),
    path("Cart",views.Cart,name="Cart"),
    path("AddToCart/<int:pk>",views.AddToCart,name="AddToCart"),
    path("IncreaseQuantity/<int:pk>",views.IncreaseQuantity,name="IncreaseQuantity"),
    path("DecreaseQuantity/<int:pk>",views.DecreaseQuantity,name="DecreaseQuantity"),
    path("DeleteCartItem/<int:pk>",views.DeleteCartItem,name="DeleteCartItem"),
     path("ProceedCheckout",views.ProceedCheckout,name="ProceedCheckout"),
    path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
    path("Success1",views.Success1,name="Success1"),
    path("MyOrderes",views.MyOrderes,name="MyOrderes"),
    path("deleteordermanu/<int:pk>",views.deleteordermanu,name="deleteordermanu"),
    path("deleteordercus/<int:pk>",views.deleteordercus,name="deleteordercus"),
    path("CheckOut",views.CheckOut,name="CheckOut"),
    path("Shop",views.Shop,name="Shop"),
    path("CustomerorederMerchant",views.CustomerorederMerchant,name="CustomerorederMerchant"),
    path("ChangeOrderStatus/<int:pk>/<str:str>",views.ChangeOrderStatus,name="ChangeOrderStatus"),
    path("ViewCustomerAddress/<int:pk>",views.ViewCustomerAddress,name="ViewCustomerAddress"),
    path("Sorting/<str:str>",views.Sorting,name="Sorting"),
    path("Sorting1/<str:str>",views.Sorting1,name="Sorting1"),
    path("Search",views.Search,name="Search"),
    path("Addreviews/<int:pk>",views.Addreviews,name="Addreviews"),
    path("ProducteditMercahant/<int:pk>",views.ProducteditMercahant,name="ProducteditMercahant"),
    path("ChangeImage/<int:pk>",views.ChangeImage,name="ChangeImage"),



    
]
