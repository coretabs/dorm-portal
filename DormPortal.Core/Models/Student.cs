﻿using System.ComponentModel.DataAnnotations;

namespace DormPortal.Core.Models
{
    public class Student : BaseEntity
	{
		[Required]
		[MaxLength(50)]
		public string FirstName { get; set; }
		public string LastName { get; set; }
		[Required]
	    public string PassportNumber { get; set; }
	}
}
