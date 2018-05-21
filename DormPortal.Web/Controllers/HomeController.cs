using Microsoft.AspNetCore.Mvc;

namespace DormPortal.Web.Controllers
{
    public class HomeController : Controller
    {
	    public IActionResult Index()
	    {
		    return View();
	    }
    }
}
