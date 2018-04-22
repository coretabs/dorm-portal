namespace DormPortal.Data
{
	public interface IUnitOfWork
    {
	    RoomRespository RoomRespository { get; }
	    StudentRepository StudentRepository { get; }
	    int Commit();
    }
}
