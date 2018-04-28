using DormPortal.Web.Helpers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ModelBinding;

namespace DormPortal.Web.Extensions
{
    public static class ModelState
    {
	    public static bool IsValid(this ModelStateDictionary modelState, out IActionResult result, object[] paramsObjects)
	    {
		    result = new OkResult();

		    foreach (var param in paramsObjects)
		    {
			    if (param == null)
			    {
					result =  new BadRequestResult();
				    return false;
			    }
		    }

		    if (!modelState.IsValid)
		    {
			    result = new UnprocessableEntityObjectResult(modelState);
			    return false;
			}

		    return true;
	    }
    }
}
