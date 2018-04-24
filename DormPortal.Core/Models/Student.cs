namespace DormPortal.Core.Models
{
    public class Student : BaseEntity
	{
	    public int Id { get; set; }
		public string Name { get; set; }
	    public string PassportNumber { get; set; }
    }
}
