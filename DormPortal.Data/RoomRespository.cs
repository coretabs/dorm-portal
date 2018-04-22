using System.Collections.Generic;
using System.Linq;
using DormPortal.Core.Models;

namespace DormPortal.Data
{
    public class RoomRespository : GenericRepository<Room>
    {
	    public RoomRespository(IQueryable<Room> dbSet) : base(dbSet)
	    {
	    }

	    public IEnumerable<Room> GetAvailableRooms()
	    {
		    return Find(room => room.IsReserved == false);
	    }

	    public bool ReserveRoom(int id)
	    {
		    var currentRoom = FindById(id);

		    currentRoom.IsReserved = true;

		    return true;
	    }
    }
}
