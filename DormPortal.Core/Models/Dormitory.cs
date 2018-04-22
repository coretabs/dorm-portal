using System.Collections.Generic;

namespace DormPortal.Core.Models
{
    public class Dormitory : IEntity
	{
	    public int Id { get; set; }
		public string Name { get; set; }
	    public ICollection<Room> Rooms { get; set; }
    }

	public interface IEntity
	{
	     int Id { get; set; }
	}
}
