using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
    public class DormitoryRespository : GenericRepository<Dormitory>
    {
	    public DormitoryRespository(DbSet<Dormitory> dbSet) : base(dbSet)
	    {
	    }
    }
}
