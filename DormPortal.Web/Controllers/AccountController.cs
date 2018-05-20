using System;
using System.Linq;
using System.Threading.Tasks;
using DormPortal.Core.Dtos;
using DormPortal.Web.Helpers;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace DormPortal.Web.Controllers
{
    public class AccountController
    {
		private readonly SignInManager<IdentityUser> _signInManager;
		private readonly UserManager<IdentityUser> _userManager;
	    private JwtTokenManager _jwtTokenManager;

	    public AccountController(UserManager<IdentityUser> userManager, SignInManager<IdentityUser> signInManager)
		{
			_userManager = userManager;
			_signInManager = signInManager;
		}

		[HttpPost]
		public async Task<object> Login([FromBody] LoginDto model)
		{
			var result = await _signInManager.PasswordSignInAsync(model.Email, model.Password, false, false);

			if (result.Succeeded)
			{
				var appUser = _userManager.Users.SingleOrDefault(r => r.Email == model.Email);
				return await _jwtTokenManager.Generate(model.Email, appUser);
			}

			throw new ApplicationException("INVALID_LOGIN_ATTEMPT");
		}

		[HttpPost]
		public async Task<object> Register([FromBody] RegisterDto model)
		{
			var user = new IdentityUser
			{
				UserName = model.Email,
				Email = model.Email
			};
			var result = await _userManager.CreateAsync(user, model.Password);

			if (result.Succeeded)
			{
				await _signInManager.SignInAsync(user, false);
				return await _jwtTokenManager.Generate(model.Email, user);
			}

			throw new ApplicationException("UNKNOWN_ERROR");
		}
	}
}
