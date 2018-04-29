using System.Linq;
using DormPortal.Core.Models;

namespace DormPortal.Web.Helpers
{
    public static class QueryableShaper
    {
	    public static IQueryable<object> Shape<T>(this IQueryable<T> data, string[] properties)
		where T: Student
	    {
		    var passportString = "PassportNumber";

		    var typeProperty = typeof(T).GetProperty(passportString);

			var result = from entity in data
			    select entity.PassportNumber;

		    return result;
	    } 
    }
}
