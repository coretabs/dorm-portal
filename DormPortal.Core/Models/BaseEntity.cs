using System.Collections;
using System.Collections.Generic;

namespace DormPortal.Core.Models
{
	public class BaseEntity : IEnumerable<BaseEntity>
	{
		public int Id { get; set; }
		public IEnumerator<BaseEntity> GetEnumerator()
		{
			yield return this;
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			return GetEnumerator();
		}
	}
}