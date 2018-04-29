using System.Linq;
using DormPortal.Data;

namespace DormPortal.Web.Helpers
{
    public static class UnitOfWorkExtension
    {
	    public static void EnsureSeedDb(this IUnitOfWork unitOfWork)
	    {
		    if (!unitOfWork.StudentRepository.GetAll().Any())
		    {
				unitOfWork.DormitoryRespository.Add(DummyData.Dormitories);
				unitOfWork.RoomRespository.Add(DummyData.Rooms);
			    unitOfWork.StudentRepository.Add(DummyData.Students);

			    unitOfWork.Commit();
		    }
		}
    }
}
