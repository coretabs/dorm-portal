namespace DormPortal.Core.Models
{
    public class Room : BaseEntity
	{
	    public BaseEntity Dormitory { get; set; }
	    public bool IsReserved { get; set; }
    }
}
