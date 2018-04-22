using System;
using DormPortal.Core.Models;

namespace DormPortal.Data
{
	public class InMemoryUnitOfWork : IUnitOfWork
	{
		private GenericRepository<Room> _roomRespository;
		private GenericRepository<Student> _studentRepository;

		public GenericRepository<T> LazyGenericRepository<T>(ref GenericRepository<T> genericRepository, params object[] args)
			where T : IEntity
		{
			genericRepository = genericRepository ??
			                    (GenericRepository<T>)Activator.CreateInstance(typeof(GenericRepository<T>), args);

			return genericRepository;
		}

		public RoomRespository RoomRespository =>
			LazyGenericRepository(ref _roomRespository, DummyData.Rooms) as RoomRespository;
			 

		public StudentRepository StudentRepository =>
			LazyGenericRepository(ref _studentRepository, DummyData.Rooms) as StudentRepository;

		public int Commit()
		{
			return 1;
		}
	}
}