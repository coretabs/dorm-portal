namespace DormPortal.Core.Models
{
    public class Room : IEntity
	{
	    public int Id { get; set; }
	    public Dormitory Dormitory { get; set; }
	    public bool IsReserved { get; set; }
    }
}
