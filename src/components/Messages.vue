<template>
  <v-app id="inspire">
    <div class="hello">
      <img src='@/assets/logo-django.png' style="width: 250px" />
      <p>The data below is added/removed from the Postgres Database using Django's ORM and Restframork.</p>
      <br/>
      <v-layout justify-center>
        
        <v-flex xs2>
          <v-text-field label="Subject" v-model="subject"></v-text-field>
          <v-text-field label="Message" v-model="msgBody"></v-text-field>
          <v-btn @click="postMessage" :disabled="!subject || !msgBody">Add</v-btn>
        </v-flex>
      </v-layout>
      
      <hr>
      <h3>Messages on Database</h3>
      <p v-if="messages.length ===0">No Messages</p>
      <div class="msg" v-for="(msg, index) in messages" :key="index">
          <p class="msg-index">[{{index}}]</p>
          <p class="msg-subject" v-html="msg.subject"></p>
          <p class="msg-body" v-html="msg.body"></p>
          <input type="submit" @click="deleteMsg(msg.pk)" value="Delete" />
      </div>
    </div>
  </v-app>
</template>

<script>
export default {
  name: "Messages",
  data() {
    return {
      subject: "",
      msgBody: "",
      messages: []
    };
  },
  mounted() {
    this.fetchMessages();
  },
  methods: {
    fetchMessages() {
      this.$backend.$fetchMessages().then(responseData => {
        this.messages = responseData;
      });
    },
    postMessage() {
      const payload = { subject: this.subject, body: this.msgBody };
      this.$backend.$postMessage(payload).then(() => {
        this.msgBody = ""
        this.subject = ""
        this.fetchMessages();
      });
    },
    deleteMsg(msgId) {
        this.$backend.$deleteMessage(msgId).then(() => {
            this.messages = this.messages.filter(m => m.pk !== msgId)
            this.fetchMessages();
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
hr {
  margin: 40px 0;
  display: block;
  height: 1px;
  border: 0;
  border-top: 1px solid #ccc;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

</style>
