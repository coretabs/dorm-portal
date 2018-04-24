using System.Collections.Generic;

namespace DormPortal.Core.Models
{
    public class Dormitory : BaseEntity
	{
		public string Name { get; set; }
	    public ICollection<Room> Rooms { get; set; }
    }
}
