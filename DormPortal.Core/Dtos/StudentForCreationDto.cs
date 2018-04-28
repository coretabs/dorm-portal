using System.ComponentModel.DataAnnotations;

namespace DormPortal.Core.Dtos
{
    public class StudentForCreationDto
    {
		[Required]
		[MaxLength(50)]
		public string FirstName { get; set; }
	    [Required]
	    [MaxLength(50)]
		public string LastName { get; set; }
	    public string PassportNumber { get; set; }
	}
}
