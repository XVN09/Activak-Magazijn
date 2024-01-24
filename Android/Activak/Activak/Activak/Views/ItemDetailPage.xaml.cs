using System.ComponentModel;
using Xamarin.Forms;
using Activak.ViewModels;

namespace Activak.Views
{
    public partial class ItemDetailPage : ContentPage
    {
        public ItemDetailPage()
        {
            InitializeComponent();
            BindingContext = new ItemDetailViewModel();
        }
    }
}
