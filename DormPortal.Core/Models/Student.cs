using System.ComponentModel.DataAnnotations;
using Sieve.Attributes;

namespace DormPortal.Core.Models
{
    public class Student : BaseEntity
	{
		[Required]
		[MaxLength(50)]
		[Sieve(CanFilter = true, CanSort = true)]
		public string FirstName { get; set; }
		[Required]
		[MaxLength(50)]
		public string LastName { get; set; }
	    public string PassportNumber { get; set; }
	}
}
