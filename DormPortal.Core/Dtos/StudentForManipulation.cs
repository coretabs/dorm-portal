using System.ComponentModel.DataAnnotations;

namespace DormPortal.Core.Dtos
{
    public abstract class StudentForManipulation
    {
		[Required]
	    [MaxLength(50)]
	    public string FirstName { get; set; }
	    [Required]
	    [MaxLength(50)]
	    public string LastName { get; set; }
	    public virtual string PassportNumber { get; set; }
	}
}
