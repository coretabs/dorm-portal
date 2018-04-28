using System.ComponentModel.DataAnnotations;

namespace DormPortal.Core.Dtos
{
    public class StudentForUpdateDto
    {
		[Required]
		[MaxLength(50)]
		public string FirstName { get; set; }
	    [Required]
		[MaxLength(50)]
		public string LastName { get; set; }
		[Required]
	    public string PassportNumber { get; set; }
	}
}
