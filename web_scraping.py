import streamlit as st
import requests

# Function to get GitHub user information using GitHub API
def get_github_user_info(github_username):
    # GitHub API URL for user data
    url = f"https://api.github.com/users/{github_username}"

    # Sending GET request to GitHub API
    response = requests.get(url)

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        user_data = response.json()

        # Extracting relevant information from the response
        name = user_data.get('name', 'Not available')
        bio = user_data.get('bio', 'Not available')
        location = user_data.get('location', 'Not available')
        followers = user_data.get('followers', 'Not available')
        following = user_data.get('following', 'Not available')
        public_repos = user_data.get('public_repos', 'Not available')
        profile_image_url = user_data.get('avatar_url', 'Not available')
        blog = user_data.get('blog', 'Not available')
        company = user_data.get('company', 'Not available')
        created_at = user_data.get('created_at', 'Not available')

        # Fetching public repositories data
        repos_url = user_data.get('repos_url', f"https://api.github.com/users/{github_username}/repos")
        repos_response = requests.get(repos_url)
        repos_data = repos_response.json()

        # Extracting repository names, descriptions, and links
        repos_list = [{'name': repo['name'], 
                       'description': repo.get('description', 'No description'), 
                       'url': repo['html_url']} for repo in repos_data]
        
        # Return all the information
        return {
            'name': name,
            'bio': bio,
            'location': location,
            'followers': followers,
            'following': following,
            'public_repos': public_repos,
            'profile_image_url': profile_image_url,
            'blog': blog,
            'company': company,
            'created_at': created_at,
            'repos': repos_list
        }
    else:
        return None

# Streamlit UI
st.title("GitHub User Information Scraper")
st.write("### Enter GitHub Username to Fetch User Information")

# User input for GitHub username
username = st.text_input("Enter GitHub Username:")

# Button to fetch data
if st.button("Fetch Info"):
    if username:
        user_info = get_github_user_info(username)

        if user_info:
            # Display the information in a structured way
            st.image(user_info['profile_image_url'], caption=f"Profile Image of {username}", use_container_width=True)
            st.subheader(f"Name: {user_info['name']}")
            st.write(f"**Bio**: {user_info['bio']}")
            st.write(f"**Location**: {user_info['location']}")
            st.write(f"**Followers**: {user_info['followers']}")
            st.write(f"**Following**: {user_info['following']}")
            st.write(f"**Public Repositories**: {user_info['public_repos']}")
            st.write(f"**Blog URL**: {user_info['blog']}")
            st.write(f"**Company**: {user_info['company']}")
            st.write(f"**Account Created On**: {user_info['created_at']}")

            # Display Repositories with name and link
            if user_info['repos']:
                st.write("### Public Repositories:")
                for repo in user_info['repos']:
                    st.write(f"**{repo['name']}**: [Link to Repo]({repo['url']}) - {repo['description']}")
            else:
                st.write("No public repositories found.")
        else:
            st.error(f"User with the username `{username}` not found or there is an issue fetching the data.")
    else:
        st.warning("Please enter a valid GitHub username.")

# Button to clear input
if st.button("Clear"):
    st.text_input("Enter GitHub Username:", value="", key="clear_input")
    st.experimental_rerun()
