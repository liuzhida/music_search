$ ->      
    class AppView extends Backbone.View
      
      el:'body'
      events:{

      } 
       
      test:->
        alert 'ok'

      initialize:->
        #console.log "initalize App"
        @upload=0 

        #window.R.bind("change",window.common.fetchBoards,window.common)
  

        @updater.poll(@)
  
      
                     
      render: =>
        #console.log "render"
        @

      updater:
        errorSleepTime:500
        timestamp:null
        poll:(context)->
          $.ajax
            url:"http://zao.fm/_rt"
            type: "POST"
            dataType: "JSON"
            timeout: 10000
            data:
              channel:channel
              timestamp:@timestamp
            success:(data)=>
              @onSuccess(data,context)
            error:(data,a,b)=>   
              @onError(data,context)
        onSuccess:(data,context)->
          try
            for command in data
              @timestamp=command.timestamp
              switch command.action
                when 'new'
                  console.log command.body
                  $('#wil-list').prepend('<ul><li class="wil-list-title">'+decodeURIComponent(command.body.title)+'</li><li class="wil-list-download"><a type="'+command.body.type+'" href="'+command.body.url+'" rel="download">下载</a></li><li class="wil-list-ctime">'+command.body.ctime+'</li></ul>')
                  window.externalCall("portal", "-videourl", command.body.url);


            @errorSleepTime = 500
            setTimeout((=> @poll(context)),0)
          catch e
            @onNonResponseError e,context

        onError:(response,context)->
          if response.status==504
            setTimeout((=> @poll(context)),0)
          else
            @errorSleepTime *= 2
            #console.log "Poll error; sleeping for #{@errorSleepTime} ms"
            setTimeout((=> @poll(context)), @errorSleepTime )
        
        onNonResponseError:(e,context)->
            @errorSleepTime *= 2;
            #console.log " #{e} Poll error; sleeping for #{@errorSleepTime} ms"
            setTimeout((=> @poll(context)),@errorSleepTime)
                          
        

    
    window.app = new AppView
