using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
	public class GenericRepository<T> where T : BaseEntity, new()
	{
		internal readonly DbSet<T> DbSet;

		public GenericRepository(DbSet<T> dbSet)
		{
			DbSet = dbSet;
		}

		public IQueryable<T> GetAll() => DbSet;

		public IQueryable<T> Find(Expression<Func<T, bool>> predicate)
		{
			return DbSet.Where(predicate);
		}

		public T FindById(int id)
		{
			var result = Find(x => x.Id == id).FirstOrDefault();

			if (result == null)
			{
				throw new KeyNotFoundException("Cannot find the entity");
			}

			return result;
		}

		public T Add(T entity) => DbSet.Add(entity).Entity;
		public T Update(T entity) => DbSet.Update(entity).Entity;
		public T Delete(T entity) => DbSet.Remove(entity).Entity;

		public void Delete(int id)
		{
			//=> DbSet.Remove(DbSet.Find(id)).Entity;
			var entity = new T { Id = id };
			DbSet.Attach(entity);
			DbSet.Remove(entity);
		}

		public IEnumerable<T> Add(IEnumerable<T> entities) => Perform(entities, Add);
		public IEnumerable<T> Update(IEnumerable<T> entities) => Perform(entities, Update);
		public IEnumerable<T> Delete(IEnumerable<T> entities) => Perform(entities, Delete);
		private IEnumerable<T> Perform(IEnumerable<T> entities, Func<T, T> operation)
			=> entities.Select(operation).ToList();
		//public void Add(IEnumerable<T> entities) => DbSet.AddRange(entities);
		//public void Update(IEnumerable<T> entities) => DbSet.UpdateRange(entities);
		//public void Delete(IEnumerable<T> entities) => DbSet.RemoveRange(entities);

		

	}
}