<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4"></div>
                <h1 class="title has-text-centered">Sign Up</h1>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default{
    name: 'SignUp', 
    data() {
        return {
            username: '', 
            password: '', 
            password2:'', 
            errors: []
        }
    }
}
</script>
