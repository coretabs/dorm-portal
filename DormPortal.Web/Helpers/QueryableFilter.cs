using System.Collections.Generic;
using System.Linq;
using Sieve.Models;
using Sieve.Services;

namespace DormPortal.Web.Extensions
{
    public static class QueryableFilter
    {
	    public static IEnumerable<T> Filter<T>(this ISieveProcessor sieveProcessor, SieveModel sieveModel, IQueryable<T> data)
	    {
		    IEnumerable<T> result;

		    if (sieveModel == null)
		    {
			    result = data.ToList();
		    }
		    else
		    {
			    result =  sieveProcessor.Apply(sieveModel, data).ToList();
		    }

		    return result;
	    }
    }
}
