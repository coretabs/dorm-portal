using DormPortal.Core.Dtos;
using DormPortal.Core.Models;
using DormPortal.Data;
using DormPortal.Web.Extensions;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;

namespace DormPortal.Web
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc().AddJsonOptions(options =>
            {
	            options.SerializerSettings.ContractResolver = new CamelCasePropertyNamesContractResolver();
	            options.SerializerSettings.ReferenceLoopHandling = ReferenceLoopHandling.Ignore;
            });

	        services.AddDbContext<DormPortalDbContext>(options => options.UseInMemoryDatabase("InMemDb"));
			services.AddScoped<IUnitOfWork, UnitOfWork>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env, IUnitOfWork unitOfWork)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
	            app.UseExceptionHandler(appBuilder => 
	            appBuilder.Run(async context =>
	            {
		            context.Response.StatusCode = 500;
		            await context.Response.WriteAsync("Something weird happened :(");
	            }));
            }

			AutoMapper.Mapper.Initialize(config =>
			{
				config.CreateMap<Student, StudentDto>();
				config.CreateMap<Student, StudentForCreationDto>();
			});

	        unitOfWork.EnsureSeedDb();

			app.UseMvc();
        }
    }
}
