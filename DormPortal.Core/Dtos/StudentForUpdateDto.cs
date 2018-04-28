using System.ComponentModel.DataAnnotations;

namespace DormPortal.Core.Dtos
{

    public class StudentForUpdateDto : StudentForManipulation
    {
	    [Required]
	    public override string PassportNumber
	    {
		    get => base.PassportNumber;
		    set => base.PassportNumber = value;
	    }
	}
}
