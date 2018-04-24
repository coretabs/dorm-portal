namespace DormPortal.Data
{
	public interface IUnitOfWork
	{
		DormitoryRespository DormitoryRespository { get; }
		RoomRespository RoomRespository { get; }
		StudentRepository StudentRepository { get; }
		bool Commit();
	}
}
