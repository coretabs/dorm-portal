namespace DormPortal.Core.Models
{
    public class Room
    {
	    public int Id { get; set; }
	    public Dormitory Dormitory { get; set; }
	    public bool IsReserved { get; set; }
    }
}
