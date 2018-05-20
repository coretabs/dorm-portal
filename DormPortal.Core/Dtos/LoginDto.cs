using System.ComponentModel.DataAnnotations;

namespace DormPortal.Core.Dtos
{
    public class LoginDto
    {
		[Required]
	    public string Email { get; set; }

	    [Required]
	    public string Password { get; set; }
	}
}
