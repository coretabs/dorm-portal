using DormPortal.Core.Dtos;
using DormPortal.Core.Models;
using DormPortal.Data;
using DormPortal.Web.Helpers;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Sieve.Services;

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
	        services.AddScoped<ISieveProcessor, SieveProcessor>();
		}

		// This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
		public void Configure(IApplicationBuilder app, IHostingEnvironment env, IUnitOfWork unitOfWork, ILoggerFactory loggerFactory)
        {
	        loggerFactory.AddConsole();
	        loggerFactory.AddDebug(LogLevel.Information);

            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
	            app.UseExceptionHandler(appBuilder => 
	            appBuilder.Run(async context =>
	            {
		            var exceptionHandlerFeature = context.Features.Get<IExceptionHandlerFeature>();
		            if (exceptionHandlerFeature != null)
		            {
			            var logger = loggerFactory.CreateLogger("Global exception logger");
			            logger.LogError(500,
				            exceptionHandlerFeature.Error,
				            exceptionHandlerFeature.Error.Message);
		            }

					context.Response.StatusCode = 500;
		            await context.Response.WriteAsync("Something weird happened :(");
	            }));
            }

			AutoMapper.Mapper.Initialize(config =>
			{
				config.CreateMap<Student, StudentDto>()
					.ForMember(studentDto => studentDto.Name, 
						options => options.MapFrom(src => $"{src.FirstName} {src.LastName}"));

				config.CreateMap<StudentForCreationDto, Student>()
					.ForMember(student => student.Id, options => options.Ignore());

				config.CreateMap<StudentForUpdateDto, Student>()
					.ForMember(student => student.Id, options => options.Ignore());
			});

	        unitOfWork.EnsureSeedDb();

			app.UseMvc();
        }
    }
}
