using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;

namespace DormPortal.Data
{
	public class GenericRepository<T> where T: BaseEntity
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

		public EntityEntry<T> Add(T entity) => DbSet.Add(entity);
		public EntityEntry<T> Update(T entity) => DbSet.Update(entity);
		public EntityEntry<T> Delete(T entity) => DbSet.Remove(entity);

		public IEnumerable<EntityEntry<T>> Add(IEnumerable<T> entities) => Perform(entities, Add);
		public IEnumerable<EntityEntry<T>> Update(IEnumerable<T> entities) => Perform(entities, Update);
		public IEnumerable<EntityEntry<T>> Delete(IEnumerable<T> entities) => Perform(entities, Delete);

		private IEnumerable<EntityEntry<T>> Perform(IEnumerable<T> entities, Func<T, EntityEntry<T>> operation)
			=> entities.Select(operation).ToList();
		
	}
}