using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace DormPortal.Web.Helpers
{
	public interface IJwtTokenManager
	{
		Task<object> Generate(string email, IdentityUser user);
	}
}